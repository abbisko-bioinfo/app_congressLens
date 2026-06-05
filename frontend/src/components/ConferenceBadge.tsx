import { Conference } from "../api/client";

interface ConferenceBadgeProps {
  conf: Conference;
}

export default function ConferenceBadge({ conf }: ConferenceBadgeProps) {
  return (
    <span className="px-2.5 py-1 bg-surface-container-high text-on-surface-variant text-[10px] rounded-full font-bold uppercase border border-outline-variant">
      {conf.acronym} {conf.year}
    </span>
  );
}