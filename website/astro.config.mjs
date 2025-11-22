// @ts-check
import { defineConfig } from "astro/config"
import starlight from "@astrojs/starlight"

// https://astro.build/config
export default defineConfig({
    site: "https://moevm4388.github.io",
    base: "/hestia",

    i18n: {
        locales: ["ru"],
        defaultLocale: "ru",
    },

    integrations: [
        starlight({
            defaultLocale: "ru",
            favicon: "/favicon.png",
            customCss: ["./src/css/theme.css"],
            title: { ru: "Hestia", en: "Hestia" },
            social: [
                {
                    icon: "github",
                    label: "GitHub",
                    href: "https://github.com/moevm4388/hestia",
                },
            ],
            sidebar: [
                {
                    label: "Web-интерфейс",
                    autogenerate: { directory: "web" },
                },
                {
                    label: "CLI",
                    autogenerate: { directory: "cli" },
                },
            ],
        }),
    ],
})
