import { Outlet } from "react-router";
import { useState } from "react";
import NavItem from "./components/NavItem";
import { navLinks } from "./components/NavLinks";
import { IoIosColorPalette } from "react-icons/io";

export default function Layout() {

  const [showColors, setShowColors] = useState(false);
  const [bg, setBg] = useState('amber')
  const colors = ["red", "orange", "amber", "yellow", "lime",
    "emerald", "teal", "cyan", "fuchsia", "pink", "rose"
  ];

  const colorClasses = {
    red: "bg-red-100", orange: "bg-orange-100", amber: "bg-amber-100",
    yellow: "bg-yellow-100", lime: "bg-lime-100", emerald: "bg-emerald-100", teal: "bg-teal-100",
    cyan: "bg-cyan-100", fuchsia: "bg-fuchsia-100", pink: "bg-pink-100", rose: "bg-rose-100",
  };

  const textClasses = {
    red: "text-red-800", orange: "text-orange-800", amber: "text-amber-800",
    yellow: "text-yellow-800", lime: "text-lime-800", emerald: "text-emerald-800", teal: "text-teal-800",
    cyan: "text-cyan-800", fuchsia: "text-fuchsia-800", pink: "text-pink-800", rose: "text-rose-800",
  };



  return (
    <div className="h-full w-full flex items-center justify-center absolute">

      <nav className="fixed left-4 bg-white/4 border border-white/20 shadow-lg backdrop-blur-md rounded-2xl flex flex-col gap-4 p-2 w-12 hover:w-32 transition-all duration-300">
        {
          navLinks.map((link) => (
            <NavItem
              key={link.path}
              name={link.name}
              path={link.path}
              icon={link.icon}
              className={`${textClasses[bg]}`}
            />
          ))
        }
      </nav>

      <main className={`h-full w-full ${colorClasses[bg]}`}>
        <Outlet />
      </main>

      <footer className="fixed right-4 bottom-4 bg-amber-900 flex items-center gap-5">
        {showColors && (
          <div
            className={`fixed left-1/2 -translate-x-1/2 bottom-4
                      bg-white shadow-lg rounded-xl px-4 py-3 flex gap-4
                        transition-all duration-300 ease-out
                        ${showColors
                ? "opacity-100 translate-y-0"
                : "opacity-0 translate-y-4 pointer-events-none"
              }
                      `}
          >
            {colors.map((color) => (
              <span
                key={color}
                className={`px-3 py-1 rounded-md bg-gray-200 text-sm font-medium
                  ${colorClasses[color]} cursor-pointer`}
                onClick={() => setBg(color)}
              >
                {color}
              </span>
            ))}
          </div>
        )}
        <button
          onClick={() => setShowColors(!showColors)}
          className={`fixed right-4 bottom-4 bg-white/30 backdrop-blur-3xl p-1 rounded-full shadow-lg cursor-pointer transition ${textClasses[bg]}`}>
          <IoIosColorPalette
            className="rounded-full text-5xl"
          />
        </button>
      </footer>

    </div>
  );
}