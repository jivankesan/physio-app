import { v } from "convex/values";
import { mutation, query } from "./_generated/server";

export const createList = mutation({
    args: {
        exerciseRefs: v.array(v.id("exercises")),
        body_location: v.string(),
      },
      handler: async (ctx, args) => {
        const { exerciseRefs, body_location } = args;
    
        const existingList = await ctx.db
          .query("exercisesList")
          .filter((q) => q.eq(q.field("body_location"), body_location))
          .first();
    
        if (existingList) {
          // Update existing list by merging and deduplicating exerciseRefs
          const updatedExerciseRefs = Array.from(
            new Set([...existingList.exerciseRefs, ...exerciseRefs])
          );
          await ctx.db.patch(existingList._id, { exerciseRefs: updatedExerciseRefs });
        } else {
          // Create a new exercisesList document
          await ctx.db.insert("exercisesList", { body_location, exerciseRefs });
        }
      },
    });

  export const getList = query({
    args: { body_location: v.string() },
  handler: async (ctx, args) => {
    const { body_location } = args;
    const exercisesList = await ctx.db
      .query("exercisesList")
      .filter((q) => q.eq(q.field("body_location"), body_location))
      .first();
    return exercisesList || null;
  },
});
