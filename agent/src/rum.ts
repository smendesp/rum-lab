import { RUMConfig, RUMInstance } from './types';
import { ClickRUM } from './clickRUM'

// Factory function para criar instância
export function createRUM(config: RUMConfig): RUMInstance {
  return new ClickRUM(config);
}

// Auto-initialization para uso direto via script tag
declare global {
  interface Window {
    __RUM_CONFIG?: RUMConfig;
    __RUM_INSTANCE?: RUMInstance;
  }
}

if (typeof window !== 'undefined') {
  const config = window.__RUM_CONFIG;
  if (config) {
    window.__RUM_INSTANCE = createRUM(config);
    window.__RUM_INSTANCE.init();
  }
}