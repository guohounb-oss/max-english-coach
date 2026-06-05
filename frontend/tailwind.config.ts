import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        background: "hsl(0 0% 4%)",
        foreground: "hsl(0 0% 93%)",
        card: "hsl(0 0% 7%)",
        "card-foreground": "hsl(0 0% 93%)",
        primary: "hsl(262 83% 58%)",
        "primary-foreground": "hsl(0 0% 100%)",
        secondary: "hsl(0 0% 12%)",
        "secondary-foreground": "hsl(0 0% 93%)",
        muted: "hsl(0 0% 15%)",
        "muted-foreground": "hsl(0 0% 60%)",
        accent: "hsl(262 83% 58%)",
        "accent-foreground": "hsl(0 0% 100%)",
        destructive: "hsl(0 84% 60%)",
        "destructive-foreground": "hsl(0 0% 100%)",
        border: "hsl(0 0% 15%)",
        ring: "hsl(262 83% 58%)",
      },
      borderRadius: {
        lg: "0.75rem",
        md: "0.5rem",
        sm: "0.25rem",
      },
    },
  },
  plugins: [],
};

export default config;
