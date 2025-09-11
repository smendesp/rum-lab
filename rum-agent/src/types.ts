export interface RUMConfig {
  appKey: string;
  apiEndpoint: string;
  sampleRate?: number;
  sessionTimeout?: number;
  maxQueueSize?: number;
  maxQueueTime?: number;
  trackClicks?: boolean;
  trackErrors?: boolean;
  trackResources?: boolean;
  trackPerformance?: boolean;
  elementList?:string[];
}

export interface RUMEvent {
  appKey: string;
  type: string;
  timestamp: number;
  sessionId: string;
  userId?: string;
  data: any;
  pageUrl: string;
  userAgent: string;
}

export interface RUMClickEvent extends RUMEvent {
  type: 'click';
  data: {
    element: string;
    text: string;
    x: number;
    y: number;
  };
}

export interface RUMErrorEvent extends RUMEvent {
  type: 'error';
  data: {
    message: string;
    stack?: string;
    filename?: string;
    lineno?: number;
    colno?: number;
  };
}

export interface RUMResourceEvent extends RUMEvent {
  type: 'resource';
  data: {
    name: string;
    type: string;
    duration: number;
    success: boolean;
    size?: number;
  };
}

export interface RUMPerformanceEvent extends RUMEvent {
  type: 'performance';
  data: {
    loadTime: number;
    domContentLoaded: number;
    firstPaint?: number | undefined;
    firstContentfulPaint?: number | undefined;
  };
}