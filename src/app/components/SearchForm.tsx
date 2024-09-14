"use client";

import { useState } from "react";
import { useAction, useMutation } from "convex/react";
import { api } from "../../../convex/_generated/api";

export default function SearchForm({
  setBodyLocation,
}: {
  setBodyLocation: (location: string) => void;
}) {
  const [bodyArea, setBodyArea] = useState("");
  const [loading, setLoading] = useState(false);

  // Action to find similar exercises based on the user's query
  const findSimilarExercises = useAction(api.exercises.similarExercises);

  // Mutation to save found exercises into the database
  const saveExercises = useMutation(api.exercisesList.createList);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    // Find exercises from the AI model (or backend)
    const exercises = await findSimilarExercises({
      descriptionQuery: bodyArea,
    });

    // Save the found exercises in the database
    await saveExercises({
      input: exercises.map((exercise) => exercise._id),
      category: bodyArea, // Tagging the exercises with body area
    });

    // Set bodyLocation in the parent to trigger the dashboard rendering
    setBodyLocation(bodyArea);

    setLoading(false);
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={bodyArea}
        onChange={(e) => setBodyArea(e.target.value)}
        placeholder="What kind of plan are you looking for today?"
      />
      <button type="submit">Generate Treatment Plan</button>
      {loading && <div>Loading...</div>}
    </form>
  );
}
