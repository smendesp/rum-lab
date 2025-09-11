import { RUMConfig, RUMEvent, RUMClickEvent, RUMErrorEvent, RUMResourceEvent, RUMPerformanceEvent } from './types';

class RealUserMonitoring {
  private config: Required<RUMConfig>;
  private sessionId: string;
  private userId: string;
  private eventQueue: RUMEvent[] = [];
  private isSending: boolean = false;

  constructor(config: RUMConfig) {
    this.config = {
      sampleRate: 1.0,
      sessionTimeout: 30 * 60 * 1000, // 30 minutos
      maxQueueSize: 100,
      maxQueueTime: 2000,
      trackClicks: true,
      trackErrors: true,
      trackResources: true,
      trackPerformance: true,
      elementList: ['BUTTON', 'A', 'INPUT', 'SELECT', 'TEXTAREA', 'I'],
      ...config
    };

    this.sessionId = this.generateSessionId();
    this.userId = this.getOrCreateUserId();
    this.initialize();
  }

  private generateSessionId(): string {
    return Math.random().toString(36).substring(2) + Date.now().toString(36);
  }

  private getOrCreateUserId(): string {
    let userId = localStorage.getItem('rum_user_id');
    if (!userId) {
      userId = Math.random().toString(36).substring(2) + Date.now().toString(36);
      localStorage.setItem('rum_user_id', userId);
    }
    return userId;
  }

  private initialize(): void {
    if (Math.random() > this.config.sampleRate) {
      return; // Não inicializa baseado no sample rate
    }

    this.setupSessionTracking();
    
    if (this.config.trackClicks) {
      this.setupClickTracking();
    }
    
    if (this.config.trackErrors) {
      this.setupErrorTracking();
    }
    
    if (this.config.trackResources) {
      this.setupResourceTracking();
    }
    
    if (this.config.trackPerformance) {
      this.setupPerformanceTracking();
    }

    this.setupBeforeUnload()

    this.setupBeaconOnUnload();
  }

  private setupSessionTracking(): void {
    // Renova sessionId após timeout
    setInterval(() => {
      this.sessionId = this.generateSessionId();
    }, this.config.sessionTimeout);
  }


  private setupBeforeUnload(): void {
    document.addEventListener("beforeunload", () => { 
      this.flushQueue()
    })

}

  private setupClickTracking(): void {
    document.addEventListener('click', (event: MouseEvent) => {
      const target = event.target as HTMLElement;
      const elementList = this.config.elementList //['BUTTON', 'A', 'INPUT', 'SELECT', 'TEXTAREA', 'I'];
      
      if (elementList.includes(target.tagName)){
        const clickEvent: RUMClickEvent = {
          appKey: this.config.appKey,
          type: 'click',
          timestamp: Date.now(),
          sessionId: this.sessionId,
          userId: this.userId,
          pageUrl: window.location.href,
          userAgent: navigator.userAgent,
          data: {
            element: target.tagName.toLowerCase(),
            text: target.textContent?.trim().substring(0, 100) || '',
            x: event.clientX,
            y: event.clientY
          }
        };

        this.queueEvent(clickEvent);
      }
    }, { capture: true, passive: true });
  }

  private setupErrorTracking(): void {
    // Captura erros globais
    window.addEventListener('error', (event: ErrorEvent) => {
      const errorEvent: RUMErrorEvent = {
        appKey: this.config.appKey,
        type: 'error',
        timestamp: Date.now(),
        sessionId: this.sessionId,
        userId: this.userId,
        pageUrl: window.location.href,
        userAgent: navigator.userAgent,
        data: {
          message: event.message,
          filename: event.filename,
          lineno: event.lineno,
          colno: event.colno,
          stack: event.error?.stack
        }
      };

      this.queueEvent(errorEvent);
    }, true);

    // Captura promises rejeitadas
    window.addEventListener('unhandledrejection', (event: PromiseRejectionEvent) => {
      const errorEvent: RUMErrorEvent = {
        appKey: this.config.appKey,
        type: 'error',
        timestamp: Date.now(),
        sessionId: this.sessionId,
        userId: this.userId,
        pageUrl: window.location.href,
        userAgent: navigator.userAgent,
        data: {
          message: event.reason?.message || 'Unhandled promise rejection',
          stack: event.reason?.stack
        }
      };

      this.queueEvent(errorEvent);
    }, true);
  }

  private setupResourceTracking(): void {
    const originalFetch = window.fetch;
    
    // Monitora fetch requests
    window.fetch = async (...args) => {
      const startTime = performance.now();
      const resourceName = typeof args[0] === 'string' ? args[0] : 'unknown';
      
      try {
        const response = await originalFetch(...args);
        const duration = performance.now() - startTime;

        const resourceEvenResourceEvent: RUMResourceEvent = {
          appKey: this.config.appKey,
          type: 'resource',
          timestamp: Date.now(),
          sessionId: this.sessionId,
          userId: this.userId,
          pageUrl: window.location.href,
          userAgent: navigator.userAgent,
          data: {
            name: resourceName,
            type: 'fetch',
            duration: Math.round(duration),
            success: response.ok,
            size: parseInt(response.headers.get('content-length') || '0')
          }
        };

        this.queueEvent(resourceEvenResourceEvent);
        return response;
      } catch (error) {
        const duration = performance.now() - startTime;
        
        const resourceEvenResourceEvent: RUMResourceEvent = {
          appKey: this.config.appKey,
          type: 'resource',
          timestamp: Date.now(),
          sessionId: this.sessionId,
          userId: this.userId,
          pageUrl: window.location.href,
          userAgent: navigator.userAgent,
          data: {
            name: resourceName,
            type: 'fetch',
            duration: Math.round(duration),
            success: false
          }
        };

        this.queueEvent(resourceEvenResourceEvent);
        throw error;
      }
    };

    // Monitora carregamento de recursos (imagens, scripts, etc.)
    const observer = new PerformanceObserver((list) => {
      list.getEntries().forEach((entry) => {
        if (entry.entryType === 'resource') {
          const resourceEntry = entry as PerformanceResourceTiming;
          
          const resourceEvent: RUMResourceEvent = {
            appKey: this.config.appKey,
            type: 'resource',
            timestamp: Date.now(),
            sessionId: this.sessionId,
            userId: this.userId,
            pageUrl: window.location.href,
            userAgent: navigator.userAgent,
            data: {
              name: resourceEntry.name,
              type: resourceEntry.initiatorType,
              duration: Math.round(resourceEntry.duration),
              success: resourceEntry.transferSize > 0,
              size: resourceEntry.transferSize
            }
          };

          this.queueEvent(resourceEvent);
        }
      });
    });

    observer.observe({ entryTypes: ['resource'] });
  }

  private setupPerformanceTracking(): void {
    window.addEventListener('load', () => {
      setTimeout(() => {
        const perfData = performance.timing;
        const paintEntries = performance.getEntriesByType('paint');
        
        const firstPaint = paintEntries.find(entry => entry.name === 'first-paint');
        const firstContentfulPaint = paintEntries.find(entry => entry.name === 'first-contentful-paint');

        const performanceEvent: RUMPerformanceEvent = {
          appKey: this.config.appKey,
          type: 'performance',
          timestamp: Date.now(),
          sessionId: this.sessionId,
          userId: this.userId,
          pageUrl: window.location.href,
          userAgent: navigator.userAgent,
          data: {
            loadTime: perfData.loadEventEnd - perfData.navigationStart,
            domContentLoaded: perfData.domContentLoadedEventEnd - perfData.navigationStart,
            firstPaint: firstPaint ? Math.round(firstPaint.startTime) : undefined,
            firstContentfulPaint: firstContentfulPaint ? Math.round(firstContentfulPaint.startTime) : undefined
          }
        };

        this.queueEvent(performanceEvent);
      }, 0);
    });
  }

  private setupBeaconOnUnload(): void {
    window.addEventListener('beforeunload', () => {
      this.flushQueue(true);
    });
  }

  private queueEvent(event: RUMEvent): void {
    this.eventQueue.push(event);
    if (this.eventQueue.length >= this.config.maxQueueSize) {
      this.flushQueue();
    } else if (this.eventQueue.length === 1) {
      // Agenda envio batch após 5 segundos
      setTimeout(() => this.flushQueue(), this.config.maxQueueTime);
    }
  }

  private async flushQueue(isBeacon: boolean = false): Promise<void> {
    if (this.isSending || this.eventQueue.length === 0) {
      return;
    }

    this.isSending = true;
    const eventsToSend = [...this.eventQueue];
    this.eventQueue = [];

    try {
      if (isBeacon && navigator.sendBeacon) {
        // Usa sendBeacon para envio durante unload
        // NAO SUPORTA HEADERS CUSTOMIZADOS
        const blob = new Blob([JSON.stringify(eventsToSend)], {
          type: 'application/json'
        });
        navigator.sendBeacon(this.config.apiEndpoint, blob);
      } else {
        // Envio normal via fetch
        await fetch(this.config.apiEndpoint, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-APP-KEY': this.config.appKey
          },
          body: JSON.stringify(eventsToSend),
          keepalive: true // Mantém a request viva mesmo após tab close
        });
      }
    } catch (error) {
      // Se falhar, recoloca os eventos na fila (exceto para beacon)
      if (!isBeacon) {
        this.eventQueue.unshift(...eventsToSend);
      }
    } finally {
      this.isSending = false;
    }
  }

  // Método público para tracking manual
  public trackCustomEvent(type: string, data: any): void {
    const customEvent: RUMEvent = {
      appKey: this.config.appKey,
      type,
      timestamp: Date.now(),
      sessionId: this.sessionId,
      userId: this.userId,
      pageUrl: window.location.href,
      userAgent: navigator.userAgent,
      data
    };

    this.queueEvent(customEvent);
  }
}

export default RealUserMonitoring;