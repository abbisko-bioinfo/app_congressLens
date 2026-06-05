export default function Footer() {
  return (
    <footer className="p-6 border-t border-outline-variant bg-surface-container-lowest mt-auto">
      <div className="flex flex-col md:flex-row justify-between items-center gap-6 max-w-[1360px] mx-auto">
        <div className="flex flex-col sm:flex-row items-center gap-2 sm:gap-4 text-center sm:text-left">
          <span className="text-primary font-bold uppercase">
            Congress Lens
          </span>
          <span className="text-on-surface-variant text-sm">
            © 2026 Conference Intelligence Systems. All rights reserved.
          </span>
        </div>
        <div className="flex flex-wrap justify-center gap-5 sm:gap-8 text-sm font-medium text-on-surface-variant">
          <a href="#" className="hover:text-primary transition-colors">
            Privacy Policy
          </a>
          <a href="#" className="hover:text-primary transition-colors">
            Terms
          </a>
          <a href="#" className="hover:text-primary transition-colors">
            Support
          </a>
        </div>
      </div>
    </footer>
  );
}