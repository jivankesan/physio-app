"use client";

import { useSearchParams } from "next/navigation";
import { useQuery } from "convex/react";
import { api } from "../../../convex/_generated/api";
import { Box, Heading, Text, Video, Spinner, Center } from "@chakra-ui/react";

export default function TreatmentPage() {
  const searchParams = useSearchParams();
  const exerciseId = searchParams.get("exerciseId");

  const exercise = useQuery(api.exercises.getExerciseById, {
    exerciseId,
  });

  if (!exercise) {
    return (
      <Center minH="100vh">
        <Spinner size="xl" />
      </Center>
    );
  }

  return (
    <Box p={8}>
      <Heading mb={4}>{exercise.name}</Heading>
      <Video
        src={exercise.videoPath} // Assuming you have a videoPath field
        controls
        width="100%"
      />
      <Text mt={4}>{exercise.description}</Text>
      {/* Additional live streaming functionality can be added here */}
    </Box>
  );
}
