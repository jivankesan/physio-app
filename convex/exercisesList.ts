import { v } from "convex/values";
import { mutation } from "./_generated/server";
import { query } from "./_generated/server";

export const createList = mutation({
    args: { input: v.array(v.id("exercises")), category: v.string() },
    handler: async (ctx, args) => {
      const exercisesList = await ctx.db.insert("exercisesList", { body_location: args.category, exerciseRefs: args.input });
      console.log(exercisesList); 
    },
  });

  export const getList = query({
    args: { body_location: v.string() },
    handler: async (ctx, args) => {
        const exercises = await ctx.db
        .query("exercisesList")
        .filter((q) => q.eq(q.field("body_location"), args.body_location))
        .collect();
        console.log(exercises);
    },
    
  });