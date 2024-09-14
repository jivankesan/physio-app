"use client";

import { useSearchParams } from "next/navigation";
import { useQuery } from "convex/react";
import { api } from "../../../convex/_generated/api";
import {
  Box,
  // Heading,
  Text,
  Spinner,
  Center,
  Button,
  Flex,
  Popover,
  PopoverTrigger,
  PopoverContent,
  PopoverArrow,
} from "@chakra-ui/react";

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

  const handleStartExercise = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
    const video = document.createElement("video");
    video.srcObject = stream;
    video.autoplay = true;
    video.playsInline = true;

    // Style to position and size the video
    video.style.position = "absolute";
    video.style.top = "0"; // Start from the top
    video.style.left = "0"; // Align to the left
    video.style.width = "66.66vw"; // Left 2/3 of the viewport
    video.style.height = "100vh"; // Full height
    video.style.zIndex = "1000";
    video.style.borderRadius = "8px";

    // Reflect the video vertically (mirror along y-axis)
    video.style.transform = "scaleX(-1)"; // Reflect vertically
    video.style.transformOrigin = "center";

    // Append the video to the document
    document.body.appendChild(video);
  };

  return (
    <Flex>
      <Box p={8} flexBasis="1/3">
        {/* Chat section */}
      </Box>
      <Box p={8} flexBasis="2/3">
        <Popover>
          <PopoverTrigger asButton>
            <Button colorScheme="blue">Start Exercise</Button>
          </PopoverTrigger>
          <PopoverContent>
            <PopoverArrow />
            <Box p={4}>
              <video
                src={exercise.file_path}
                controls
                width="100%"
                height="auto"
              />
              <Button
                colorScheme="red"
                size="sm"
                mt={2}
                onClick={handleStartExercise}
              >
                Close
              </Button>
            </Box>
          </PopoverContent>
        </Popover>
      </Box>
    </Flex>
  );
}
