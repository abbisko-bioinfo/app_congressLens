import { useQuery } from "@tanstack/react-query";
import { api } from "../api/client";
import type { Presentation } from "../api/client";
import PageShell from "../components/PageShell";
import PresentationTable from "../components/PresentationTable";
import { useAuth } from "../hooks/useAuth";

export default function StarPage() {
  const { isAuthenticated } = useAuth();

  const { data: watchlist } = useQuery({
    queryKey: ["watchlist"],
    queryFn: () => api.watchlist.list(),
    enabled: isAuthenticated,
  });

  const watchedPresentationIds =
    watchlist
      ?.filter((w) => w.target_type === "presentation")
      .map((w) => w.target_id) ?? [];

  const { data: presData } = useQuery({
    queryKey: ["presentations", "starred"],
    queryFn: () =>
      api.presentations.list({
        limit: "100",
      }),
    enabled: isAuthenticated,
  });

  const starredPresentations: Presentation[] =
    presData?.items?.filter((p) =>
      watchedPresentationIds.includes(p.id)
    ) ?? [];

  // Get default congress from first starred presentation
  const defaultCongress =
    starredPresentations.length > 0
      ? starredPresentations[0].conference_id
      : "";

  if (!isAuthenticated) {
    return (
      <main
        className="flex-1 p-5 sm:p-8 lg:p-10 max-w-[1360px] mx-auto w-full"
      >
        <div
          className="flex flex-col items-center justify-center py-20 text-on-surface-variant"
        >
          <span className="material-symbols-outlined text-4xl mb-4">
            lock
          </span>
          <p className="text-lg font-semibold">
            Login to star presentations
          </p>
          <p className="text-sm mt-2">
            Authenticate with your LDAP account to access your watchlist.
          </p>
        </div>
      </main>
    );
  }

  return (
    <PageShell
      title="Starred Presentations"
      subtitle="Current user followed presentation list, replacing the old archives page."
      congress={defaultCongress}
    >
      <PresentationTable
        rows={starredPresentations}
        congress={defaultCongress}
        showConference={true}
      />
    </PageShell>
  );
}