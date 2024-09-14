/*
import { query, mutation } from "./_generated/server";
import { v } from "convex/values";
import { internal } from "./_generated/api";

export const createTreatmentPlan = mutation({
  args: {
    descriptionQuery: v.string(),
    bodyLocation: v.string(),
  },
  handler: async (ctx, args) => {
    const exercises = await ctx.runAction(internal.exercises.similarExercises, {
      descriptionQuery: args.descriptionQuery,
      bodyLocation: args.bodyLocation,
    });

    const treatmentPlan = {
      exercises: exercises.map(exercise => exercise._id),
      createdAt: new Date().toISOString(),
    };

    return await ctx.db.insert("treatmentPlans", treatmentPlan);
  },
});

export const get = query({
  args: {},
  handler: async (ctx) => {
    const treatmentPlans = await ctx.db.query("treatmentPlans").collect();
    return Promise.all(treatmentPlans.map(async (plan) => {
      const exercises = await Promise.all(
        plan.exercises.map(id => ctx.db.get(id))
      );
      return { ...plan, exercises };
    }));
  },
});

*/