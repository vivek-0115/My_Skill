import { Link, useLocation } from 'react-router'
import React from 'react'

export default function NavItem({ name, path, icon: Icon, className="" }) {

    const location = useLocation();
    const isActive = location.pathname === path;

    return (
        <Link
            to={path}
            className={`rounded-lg p-2 transition border-0 flex items-center gap-2
            ${isActive
                    ? ` ${className}`
                    : "hover:bg-white/80 hover:shadow-2xl text-gray-700"
                }  overflow-hidden whitespace-nowrap hover:max-w-xs transition-all duration-300`}
        >
            <Icon className="text-lg shrink-0" />
            <span>
                {name}
            </span>
        </Link>
    )
}
