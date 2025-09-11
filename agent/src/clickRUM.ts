import { RUMConfig, ClickEventData, RUMInstance } from './types';

export class ClickRUM implements RUMInstance {
  private config: Required<RUMConfig>;
  private isInitialized = false;
  private userMetadata: Record<string, any> = {};
  private clickHandler: ((event: MouseEvent) => void) | null = null;

  constructor(config: RUMConfig) {
    this.config = {
      sampleRate: 1.0,
      debug: true,
      ignoreSelectors: ['[data-rum-ignore]', '.rum-ignore'],
      customMetadata: {},
      beforeSend: (data) => data,
      ...config,
    };

    this.validateConfig();
  }

  private validateConfig(): void {
    if (!this.config.endpoint) {
      throw new Error('Endpoint is required for RUM configuration');
    }

    if (this.config.sampleRate < 0 || this.config.sampleRate > 1) {
      throw new Error('Sample rate must be between 0 and 1');
    }
  }

  public init(): void {
    if (this.isInitialized) {
      this.log('RUM already initialized');
      return;
    }

    // if (Math.random() > this.config.sampleRate) {
    //   this.log('Skipping initialization due to sample rate');
    //   return;
    // }

    this.setupEventListeners();
    this.isInitialized = true;

    this.log('RUM initialized successfully');
  }

  public destroy(): void {
    if (this.clickHandler) {
      document.removeEventListener('click', this.clickHandler);
      this.clickHandler = null;
    }
    this.isInitialized = false;
    this.log('RUM destroyed');
  }

  public setUserMetadata(metadata: Record<string, any>): void {
    this.userMetadata = { ...this.userMetadata, ...metadata };
  }

  public trackCustomEvent(eventName: string, data?: Record<string, any>): void {
    const eventData: ClickEventData = {
      appKey: this.config.appKey,
      eventType: `custom:${eventName}`,
      timestamp: Date.now(),
      element: {
        tagName: 'CUSTOM_EVENT',
      },
      position: { x: 0, y: 0 },
      page: this.getPageData(),
      user: this.getUserData(),
      metadata: data,
    };

    this.sendData(eventData);
  }

  private setupEventListeners(): void {
    this.clickHandler = this.handleClick.bind(this);
    document.addEventListener('click', this.clickHandler, {
      capture: true,
      passive: true,
    });
  }

  private handleClick(event: MouseEvent): void {
    try {
      const target = event.target as HTMLElement;
      
      if (this.shouldIgnoreElement(target)) {
        return;
      }

      // Encontra o elemento mais próximo que é um botão ou link
      const interactiveElement = this.findInteractiveElement(target);
      if (!interactiveElement) return;

      const eventData = this.createEventData(interactiveElement, event);
      this.sendData(eventData);

    } catch (error) {
      this.logError('Error handling click event', error);
    }
  }

  private shouldIgnoreElement(element: HTMLElement): boolean {
    // Verifica se o elemento ou seus pais devem ser ignorados
    return this.config.ignoreSelectors.some(selector => 
      element.matches(selector) || element.closest(selector)
    );
  }

  private findInteractiveElement(element: HTMLElement): HTMLElement | null {
    const interactiveTags = ['BUTTON', 'A', 'INPUT', 'SELECT', 'TEXTAREA', 'I'];
    let currentElement: HTMLElement | null = element;

    while (currentElement && currentElement !== document.body) {
      if (interactiveTags.includes(currentElement.tagName)) {
        return currentElement;
      }
      currentElement = currentElement.parentElement;
    }

    return null;
  }

  private createEventData(element: HTMLElement, event: MouseEvent): ClickEventData {
    return {
      appKey: this.config.appKey,
      eventType: 'click',
      timestamp: Date.now(),
      element: {
        tagName: element.tagName,
        id: element.id || undefined,
        classes: element.className ? element.className.split(' ').filter(Boolean) : undefined,
        text: this.getElementText(element),
        href: element.getAttribute('href') || undefined,
        type: element.getAttribute('type') || undefined,
        name: element.getAttribute('name') || undefined,
        value: (element as HTMLInputElement).value || undefined,
      },
      position: {
        x: event.clientX,
        y: event.clientY,
      },
      page: this.getPageData(),
      user: this.getUserData(),
      metadata: {
        ...this.config.customMetadata,
        ...this.userMetadata,
      },
    };
  }

  private getElementText(element: HTMLElement): string {
    try {
      return element.textContent?.trim().substring(0, 100) || '';
    } catch {
      return '';
    }
  }

  private getPageData() {
    return {
      url: window.location.href,
      title: document.title,
      referrer: document.referrer,
    };
  }

  private getUserData() {
    return {
      agent: navigator.userAgent,
      language: navigator.language,
      timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
    };
  }

  private async sendData(data: ClickEventData): Promise<void> {
    try {
      // Aplica hook beforeSend
      let processedData = this.config.beforeSend?.(data) || data;
      if (!processedData) return;

      if (this.config.debug) {
        console.log('RUM Event:', processedData);
      }

      // Usa navigator.sendBeacon para melhor performance
      const blob = new Blob([JSON.stringify(processedData)], {
        type: 'application/json',
      });

      if (!navigator.sendBeacon(this.config.endpoint, blob)) {
        // Fallback para fetch
        fetch(this.config.endpoint, {
          method: 'POST',
          body: JSON.stringify(data),
          headers: { 'Content-Type': 'application/json' },
          keepalive: true
        });
      }
    } catch (error) {
      this.logError('Error sending RUM data', error);
    }
  }

  private log(message: string): void {
    if (this.config.debug) {
      console.log(`[RUM] ${message}`);
    }
  }

  private logError(message: string, error: any): void {
    console.error(`[RUM Error] ${message}:`, error);
  }
}
