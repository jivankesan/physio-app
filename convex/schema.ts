import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
  exercises: defineTable({
    description: v.string(),
    file_path: v.string(),
    body_location: v.string(),
    embedding: v.array(v.number()),
    ref_angle: v.array(v.array(v.number())),
  }).vectorIndex("by_embedding", {
    vectorField: "embedding",
    dimensions: 24,
    filterFields: ["body_location"],
  }),
  exercisesList: defineTable({
    body_location: v.string(),    // Tag for treatment plan
    exerciseRefs: v.array(v.id("exercises")), // References to exercises in the exercises table
  }),
});