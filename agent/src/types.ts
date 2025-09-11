export interface RUMConfig {
  appKey: string;
  endpoint: string;
  sampleRate?: number;
  debug?: boolean;
  ignoreSelectors?: string[];
  customMetadata?: Record<string, any>;
  beforeSend?: (data: ClickEventData) => ClickEventData | null;
}

export interface ClickEventData {
  appKey: string;
  eventType: string;
  timestamp: number;
  element: {
    tagName: string;
    id?: string;
    classes?: string[];
    text?: string;
    href?: string;
    type?: string;
    name?: string;
    value?: string;
  };
  position: {
    x: number;
    y: number;
  };
  page: {
    url: string;
    title: string;
    referrer: string;
  };
  user: {
    agent: string;
    language: string;
    timezone: string;
  };
  metadata?: Record<string, any>;
}

export interface RUMInstance {
  init: () => void;
  destroy: () => void;
  trackCustomEvent: (eventName: string, data?: Record<string, any>) => void;
  setUserMetadata: (metadata: Record<string, any>) => void;
}