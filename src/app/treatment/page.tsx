"use client";

import { useSearchParams } from "next/navigation";
import { useQuery } from "convex/react";
import { api } from "../../../convex/_generated/api";
import { Box, Heading, Text, Spinner, Center, Button } from "@chakra-ui/react";

export default function TreatmentPage() {
  const searchParams = useSearchParams();
  const exerciseId = searchParams.get("exerciseId");

  // Fetch the exercise by ID
  const exercise = useQuery(api.exercises.getExerciseById, {
    exerciseId: exerciseId,
  });

  if (exercise === undefined) {
    return (
      <Center minH="100vh">
        <Spinner size="xl" />
      </Center>
    );
  }

  if (!exercise) {
    return (
      <Center minH="100vh">
        <Text>Exercise not found.</Text>
      </Center>
    );
  }

  return (
    <Box p={8}>
      <Heading mb={4}>{exercise.description}</Heading>
      <Box
        as="video"
        src={exercise.file_path}
        controls
        width="100%"
        height="auto"
      />
      <Text mt={4}>{exercise.description}</Text>
      {/* Add additional functionality like progress tracking here */}
      <Button
        mt={4}
        colorScheme="blue"
        onClick={() => alert("Training Started!")}
      >
        Start Exercise
      </Button>
    </Box>
  );
}
