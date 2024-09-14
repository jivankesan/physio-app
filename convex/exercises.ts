import { v } from "convex/values";
import { action, internalQuery, query} from "./_generated/server";
import { internal } from "./_generated/api";
import { Doc } from "./_generated/dataModel";
import { CohereClient } from "cohere-ai";

const cohere = new CohereClient({
  token: "aJj0xHpb5VNBR6yWsnJxLffGM4dVVVLEkXhJjYpT",
});

export const fetchResults = internalQuery({
  args: { ids: v.array(v.id("exercises")) },
  handler: async (ctx, args) => {
    const results = [];
    for (const id of args.ids) {
      const doc = await ctx.db.get(id);
      if (doc === null) {
        continue;
      }
      results.push(doc);
    }
    return results;
  },
});

export const similarExercises = action({
  args: {
    descriptionQuery: v.string(),
  },
  handler: async (ctx, args) => {
    
    const embedding = await cohere.embed({texts: [args.descriptionQuery], model:'embed-english-light-v3.0', inputType: 'classification' }) as { embeddings: number[][]};
    const body_location = "elbow"; // cohere.chat();
    // 2. Then search for similar foods!
    const results = await ctx.vectorSearch("exercises", "by_embedding", {
      vector: embedding["embeddings"][0],
      limit: 16,
      filter: (q) => q.eq("body_location", body_location ),
    });
    // 3. Fetch the results
    const exercises: Array<Doc<"exercises">> = await ctx.runQuery(
      internal.exercises.fetchResults,
      { ids: results.map((result) => result._id) },
    );
    return exercises;
  },
});

export const getExercisesByIds = query({
  args: { exerciseIds: v.array(v.id("exercises")) },
  handler: async (ctx, args) => {
    const { exerciseIds } = args;
    if (!exerciseIds || exerciseIds.length === 0) {
      return [];
    }
    const exercises = await Promise.all(exerciseIds.map(id => ctx.db.get(id)));
    return exercises.filter((exercise) => exercise !== null);
  },
});

// Internal query to get a single exercise by ID
export const getExerciseById = query({
  args: { exerciseId: v.id("exercises") },
  handler: async (ctx, args) => {
    const { exerciseId } = args;
    const exercise = await ctx.db.get(exerciseId);
    return exercise || null;
  },
});
