import { v } from "convex/values";
import { action, internalQuery, query} from "./_generated/server";
import { internal } from "./_generated/api";
import { Doc } from "./_generated/dataModel";


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
    embedding: v.array(v.float64()),
  },
  handler: async (ctx, args) => {
    const { embedding } = args; // Extracting args to use them
    
    // Assuming embedding is already processed and ready for use
    const body_location = "Hip"; // cohere.chat();
    
    // 2. Then search for similar exercises!
    const results = await ctx.vectorSearch("exercises", "by_embedding", {
      vector: embedding, 
      limit: 4,
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
