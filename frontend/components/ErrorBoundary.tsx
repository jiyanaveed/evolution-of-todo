import React from 'react';

interface ErrorBoundaryState {
  hasError: boolean;
  error?: Error;
}

interface ErrorBoundaryProps {
  children: React.ReactNode;
  fallback?: React.ComponentType<{ error?: Error }>;
}

class ErrorBoundary extends React.Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error('Error caught by boundary:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      const FallbackComponent = this.props.fallback || DefaultErrorFallback;
      return <FallbackComponent error={this.state.error} />;
    }

    return this.props.children;
  }
}

const DefaultErrorFallback = ({ error }: { error?: Error }) => (
  <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-4">
    <h2 className="text-lg font-semibold text-red-800">Something went wrong</h2>
    {error && <p className="text-red-600 mt-2">{error.message}</p>}
    <p className="text-red-600 mt-2">Please refresh the page to try again.</p>
  </div>
);

export default ErrorBoundary;