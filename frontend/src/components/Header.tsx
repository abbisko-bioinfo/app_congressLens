import { Link, useLocation } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";

const NAV_ITEMS = [
  { pathPrefix: "/session", label: "sessions", icon: "list_alt" },
  { pathPrefix: "/presentations", label: "presentations", icon: "table_view" },
  { pathPrefix: "/star", label: "star", icon: "star" },
];

export default function Header() {
  const location = useLocation();
  const { user, isAuthenticated } = useAuth();

  // Extract congress param from current route for nav links
  const navCongress = location.pathname.split("/")[2] || "";
  const active = (keys: string[]) =>
    keys.some(
      (k) =>
        location.pathname === k ||
        location.pathname.startsWith(k + "/")
    );

  // Build congress-aware nav paths
  const getNavPath = (prefix: string) => {
    if (prefix === "/star") return "/star";
    return navCongress ? `${prefix}/${navCongress}` : prefix;
  };

  return (
    <header className="w-full sticky top-0 z-50 bg-surface/95 backdrop-blur-md border-b border-outline-variant">
      <div className="flex flex-col lg:flex-row lg:justify-between lg:items-center px-5 sm:px-8 py-3 lg:h-16 gap-3 border-b border-outline-variant/30">
        <div className="flex flex-col sm:flex-row sm:items-center gap-3 sm:gap-6 min-w-0 w-full lg:w-auto">
          <Link to="/" className="flex flex-col shrink-0">
            <span className="text-xl font-extrabold text-primary leading-tight uppercase font-headline">
              Congress Lens
            </span>
            <p className="text-[10px] text-secondary font-semibold uppercase font-label">
              Conference Intelligence
            </p>
          </Link>
          <div className="h-8 w-px bg-outline-variant hidden md:block"></div>
          <nav className="flex items-center h-11 lg:h-16 gap-1 overflow-x-auto custom-scrollbar w-full">
            {NAV_ITEMS.map((item) => (
              <Link
                key={item.pathPrefix}
                to={getNavPath(item.pathPrefix)}
                className={`flex shrink-0 items-center gap-2 px-3 sm:px-4 h-full transition-all text-sm font-medium border-b-2 ${
                  active([item.pathPrefix])
                    ? "text-primary border-primary"
                    : "text-on-surface-variant border-transparent hover:text-primary"
                }`}
              >
                <span className="material-symbols-outlined text-xl">
                  {item.icon}
                </span>
                <span>{item.label}</span>
              </Link>
            ))}
          </nav>
        </div>

        <div className="flex items-center justify-between lg:justify-end gap-2 shrink-0 w-full lg:w-auto">
          <div className="hidden lg:flex items-center bg-surface-container-low rounded px-3 py-1.5 border border-outline-variant w-56 focus-within:border-primary transition-colors">
            <span className="material-symbols-outlined text-on-surface-variant text-sm">
              search
            </span>
            <input
              className="bg-transparent border-none focus:ring-0 text-sm w-full placeholder:text-outline text-on-surface"
              placeholder="Search presentations..."
              type="text"
            />
          </div>
          <button className="material-symbols-outlined text-on-surface-variant hover:text-secondary transition-colors p-1.5 rounded">
            notifications
          </button>
          <button className="material-symbols-outlined text-on-surface-variant hover:text-secondary transition-colors p-1.5 rounded">
            settings
          </button>
          {isAuthenticated && user ? (
            <div className="flex items-center gap-2 hover:bg-surface-container-high p-1 pr-2 rounded-xl transition-colors cursor-pointer border border-transparent hover:border-outline-variant">
              <div className="w-8 h-8 rounded-full bg-primary text-on-primary flex items-center justify-center text-xs font-bold border-2 border-primary-container">
                {user.display_name
                  .split(" ")
                  .map((n) => n[0])
                  .join("")
                  .slice(0, 2)
                  .toUpperCase()}
              </div>
              <span className="text-sm font-semibold text-on-surface hidden sm:inline">
                {user.display_name}
              </span>
            </div>
          ) : (
            <div className="flex items-center gap-2 hover:bg-surface-container-high p-1 pr-2 rounded-xl transition-colors cursor-pointer border border-transparent hover:border-outline-variant">
              <div className="w-8 h-8 rounded-full bg-neutral-steel text-on-surface flex items-center justify-center">
                <span className="material-symbols-outlined text-sm">
                  person
                </span>
              </div>
              <span className="text-sm font-semibold text-on-surface-variant hidden sm:inline">
                Login
              </span>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}