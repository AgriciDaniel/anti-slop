import { QuartzConfig } from "@quartz-org/quartz"

const config: QuartzConfig = {
  configuration: {
    pageTitle: "Anti-Slop Brain",
    enableSPA: true,
    enablePopovers: true,
    analytics: null,
    locale: "en-US",
    baseUrl: "",
    ignorePatterns: [
  ".raw/**",
  ".raw",
  ".obsidian",
  "hot.md",
  "log.md",
  "references/source-ledger.json",
  "references/claim-ledger.md"
],
    defaultDateType: "modified",
    theme: {
      typography: {
        header: "Inter",
        body: "Source Sans Pro",
        code: "IBM Plex Mono",
      },
      cdnCaching: true,
      colors: {
        lightMode: {
          light: "#ffffff",
          lightgray: "#f5f5f5",
          gray: "#e5e7eb",
          darkgray: "#4b5563",
          dark: "#111827",
          secondary: "#2563eb",
          tertiary: "#16a34a",
          highlight: "rgba(250, 204, 21, 0.25)",
          textHighlight: "#fff7cc",
        },
        darkMode: {
          light: "#111827",
          lightgray: "#1f2937",
          gray: "#374151",
          darkgray: "#d1d5db",
          dark: "#f9fafb",
          secondary: "#60a5fa",
          tertiary: "#4ade80",
          highlight: "rgba(250, 204, 21, 0.18)",
          textHighlight: "#3b2f00",
        },
      },
    },
  },
  plugins: {},
}

export default config
