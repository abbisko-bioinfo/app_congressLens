import { useParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { api } from "../api/client";
import type { Conference, Presentation } from "../api/client";
import PageShell from "../components/PageShell";
import PresentationTable from "../components/PresentationTable";

function getCongressId(conf: Conference): string {
  return conf.acronym.toLowerCase().replace(/\s+/g, "") + "-" + conf.year;
}

export default function PresentationList() {
  const { congress } = useParams<{ congress: string }>();

  const { data: confData } = useQuery({
    queryKey: ["conferences"],
    queryFn: () => api.conferences.list(),
  });

  const conferences: Conference[] = confData?.items ?? [];
  const conf = conferences.find((c) => getCongressId(c) === congress);

  const { data } = useQuery({
    queryKey: ["presentations", conf?.id],
    queryFn: () =>
      api.presentations.list({
        conference_id: conf?.id ?? "",
        limit: "200",
      }),
    enabled: !!conf,
  });

  const rows: Presentation[] = data?.items ?? [];

  return (
    <PageShell
      title="Presentations"
      subtitle="All presentation records are displayed as a table, with drill-down detail pages for text, attachments and user comments."
      congress={congress}
    >
      <PresentationTable rows={rows} congress={congress ?? ""} />
    </PageShell>
  );
}