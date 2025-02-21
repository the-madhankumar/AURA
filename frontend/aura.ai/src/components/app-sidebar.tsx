"use client";

import { JSX, useState } from "react";
import { FiMenu, FiHome, FiMessageSquare, FiSettings } from "react-icons/fi";
import Link from "next/link";

const Sidebar = () => {
  const [isOpen, setIsOpen] = useState(true);

  return (
    <div className="flex h-screen">
      {/* Sidebar */}
      <div className={`bg-gray-900 text-white h-full transition-all ${isOpen ? "w-60" : "w-16"}`}>
        <button
          onClick={() => setIsOpen(!isOpen)}
          className="p-4 text-gray-400 hover:text-white transition"
        >
          <FiMenu size={24} />
        </button>

        {/* Menu Items */}
        <nav className="mt-4 space-y-4">
          <SidebarItem href="/" icon={<FiHome />} label="Home" isOpen={isOpen} />
          <SidebarItem href="/chat" icon={<FiMessageSquare />} label="Chat" isOpen={isOpen} />
          <SidebarItem href="/settings" icon={<FiSettings />} label="Settings" isOpen={isOpen} />
        </nav>
      </div>

    </div>
  );
};

const SidebarItem = ({ href, icon, label, isOpen }: { href: string; icon: JSX.Element; label: string; isOpen: boolean }) => (
  <Link href={href} className="flex items-center space-x-4 px-4 py-3 hover:bg-gray-800 transition rounded-lg">
    <span className="text-xl">{icon}</span>
    {isOpen && <span className="text-sm font-medium">{label}</span>}
  </Link>
);

export default Sidebar;
