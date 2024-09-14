"use client";

import { useQuery } from "convex/react";
import { api } from "../../../convex/_generated/api"; // Adjusted import path

export default function DashboardPage({
  bodyLocation,
}: {
  bodyLocation: string;
}) {
  // Query to retrieve exercises stored for the given body location
  const exercises =
    useQuery(api.exercisesList.getList, { body_location: bodyLocation }) || []; // Ensure exercises is an array

  return (
    <div>
      <h1>Dashboard</h1>

      {exercises.length > 0 ? ( // Check if exercises has items
        exercises.map((exercise: { _id: string; description: string }) => (
          <div key={exercise._id}>
            <p>{exercise.description}</p>
          </div>
        ))
      ) : (
        <p>No exercises found yet</p>
      )}
    </div>
  );
}
