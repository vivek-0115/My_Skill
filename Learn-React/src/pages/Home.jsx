export default function Home() {
  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="max-w-3xl bg-white/20 backdrop-blur-lg rounded-2xl shadow-lg p-8">
        {/* Title */}
        <h1 className="text-4xl font-bold text-gray-800 mb-4">
          Learn React & Next.js
        </h1>

        {/* Subtitle */}
        <p className="text-gray-600 mb-6">
          A simple learning space to understand modern frontend development,
          routing, components, and full-stack integration.
        </p>

        {/* Learning Goals */}
        <div className="mb-2">
          <h2 className="text-xl font-semibold text-gray-700 mb-3">
            What I’ll learn
          </h2>
          <ul className="list-disc list-inside text-gray-600 space-y-1">
            <li>React components & hooks</li>
            <li>Routing & layouts</li>
            <li>Next.js fundamentals</li>
            <li>API integration with backend</li>
          </ul>
        </div>
      </div>
    </div>
  );
}
