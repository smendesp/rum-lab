import RealUserMonitoring from './rum';
import { RUMConfig } from './types';

// Exportação para uso global
declare global {
  interface Window {
    __RUM?: RealUserMonitoring;
    __RUM_CONFIG?: RUMConfig;    
  }
}

// Inicialização automática se configurado via data attributes
function autoInitialize(): void {
  const scriptElement = document.currentScript as HTMLScriptElement;
  const configAttr = scriptElement?.getAttribute('data-config');
  const configRum = window.__RUM_CONFIG;
  
  try {
    const config = (configAttr === null ? configRum : JSON.parse(configAttr))
    window.__RUM = new RealUserMonitoring(config);
  } catch (error) {
    console.error('Failed to parse RUM configuration:', error);
  }
  
}

// Exportações
export type { RUMConfig };
export { RealUserMonitoring };
export default RealUserMonitoring;

// Inicialização automática se executado no browser
if (typeof window !== 'undefined') {
  autoInitialize();
}