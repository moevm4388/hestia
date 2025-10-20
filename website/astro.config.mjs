// @ts-check
import { defineConfig } from "astro/config"
import starlight from "@astrojs/starlight"

// https://astro.build/config
export default defineConfig({
    i18n: {
        locales: ["ru"],
        defaultLocale: "ru",
    },

    integrations: [
        starlight({
            defaultLocale: "ru",
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
                    label: "Guides",
                    items: [
                        // Each item here is one entry in the navigation menu.
                        { label: "Example Guide", slug: "guides/example" },
                    ],
                },
                {
                    label: "Reference",
                    autogenerate: { directory: "reference" },
                },
            ],
        }),
    ],
})
