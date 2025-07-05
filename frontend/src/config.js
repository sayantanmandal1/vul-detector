// Configuration file for API endpoints
const config = {
  // Production API URL
  API_BASE_URL: 'https://vul-detector.onrender.com',
  
  // Development API URL (for local development)
  // API_BASE_URL: 'http://localhost:8000',
  
  // API endpoints
  ENDPOINTS: {
    ANALYZE_CODE: '/analyze/code',
    ANALYZE_REPO: '/analyze/repo',
    REPORT: '/report',
    HEALTH: '/health'
  }
};

// Helper function to get full API URL
export const getApiUrl = (endpoint) => {
  return `${config.API_BASE_URL}${endpoint}`;
};

export default config; 