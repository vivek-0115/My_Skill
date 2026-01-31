import {createBrowserRouter, RouterProvider} from 'react-router'
import { createRoot } from 'react-dom/client'
import { StrictMode } from 'react'
import App from './App.jsx'
import Layout from "./Layout";
import Home from './pages/Home.jsx';
import Counter from "./pages/Counter";
import PassGen from "./pages/PassGen";
import Settings from "./pages/Settings";

const router = createBrowserRouter([
  {
    path: "/",
    element: <Layout />,
    children: [
      { index: true, element: <Home /> },
      { path: "counter", element: <Counter /> },
      { path: "password-generator", element: <PassGen /> },
      { path: "settings", element: <Settings /> },
    ],
  },
]);

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <RouterProvider router={router}/>
  </StrictMode>,
)
