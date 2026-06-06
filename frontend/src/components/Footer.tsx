export default function Footer() {
  return (
    <footer className="p-6 border-t border-outline-variant bg-surface-container-lowest mt-auto">
      <div className="flex flex-col md:flex-row justify-between items-center gap-6 max-w-[1360px] mx-auto">
        <div className="flex flex-col sm:flex-row items-center gap-2 sm:gap-4 text-center sm:text-left">
          <span className="text-on-surface-variant text-sm">
            Copyright © 2026 All rights reserved:{" "}
            <a
              href="https://www.abbisko.com/"
              target="_blank"
              rel="noreferrer"
              className="ml-1 underline underline-offset-2 hover:text-primary"
            >
              Abbisko Therapeautics
            </a>
          </span>
        </div>
      </div>
    </footer>
  );
}
