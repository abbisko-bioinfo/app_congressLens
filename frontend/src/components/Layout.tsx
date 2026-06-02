import { Link, Outlet, useLocation } from "react-router-dom";

const NAV_ITEMS = [
  { path: "/", label: "Dashboard" },
  { path: "/conferences", label: "Conferences" },
  { path: "/presentations", label: "Presentations" },
  { path: "/calendar", label: "Calendar" },
];

export default function Layout() {
  const location = useLocation();

  return (
    <div className="min-h-screen bg-gray-50 flex">
      <nav className="w-48 bg-white border-r border-gray-200 p-4 space-y-2">
        <div className="text-lg font-bold text-gray-900 mb-4">CongressLens</div>
        {NAV_ITEMS.map((item) => (
          <Link
            key={item.path}
            to={item.path}
            className={`block px-3 py-2 rounded-md text-sm transition-colors ${location.pathname === item.path ? "bg-blue-50 text-blue-700 font-medium" : "text-gray-600 hover:bg-gray-100"}`}
          >
            {item.label}
          </Link>
        ))}
      </nav>
      <main className="flex-1 overflow-auto">
        <Outlet />
      </main>
    </div>
  );
}