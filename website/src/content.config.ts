import { defineCollection } from "astro:content"
import { file } from "astro/loaders"
import { docsLoader } from "@astrojs/starlight/loaders"
import { docsSchema } from "@astrojs/starlight/schema"
import { z } from "astro:schema"

const comments = defineCollection({
    loader: file("./src/content/comments/comments.yaml"),
    schema: z.object({
        id: z.number().positive(),
        name: z.string(),
        login: z.string(),
        body: z.string(),
        avatar: z.string().url(),
        href: z.string().url(),
    }),
})

const docs = defineCollection({ loader: docsLoader(), schema: docsSchema() })

export const collections = { comments, docs }
