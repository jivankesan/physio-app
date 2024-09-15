"use client";

import { useSearchParams } from "next/navigation";
import { useQuery } from "convex/react";
import { api } from "../../../convex/_generated/api";
import {
  Box,
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
    exerciseId: exerciseId || null,
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
    console.log("Starting exercise");
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

    // Create a close button
    const closeButton = document.createElement("button");
    closeButton.textContent = "X";
    closeButton.style.position = "absolute";
    closeButton.style.top = "10px"; // Position at the top
    closeButton.style.right = "10px"; // Align to the right
    closeButton.style.zIndex = "1001"; // Ensure it's on top of the video
    closeButton.style.cursor = "pointer";
    closeButton.onclick = () => {
      document.body.removeChild(video);
      document.body.removeChild(closeButton);
      stream.getTracks().forEach((track) => track.stop());
    };
    document.body.appendChild(closeButton);

    // Buffer to store frames for 2 seconds
    const frameBuffer: Blob[] = [];
    let lastFrameTime = 0;

    // Function to process video frames
    const processVideo = () => {
      if (video.readyState === video.HAVE_ENOUGH_DATA) {
        console.log("Processing video frames");

        const canvas = document.createElement("canvas");
        const ctx = canvas.getContext("2d");

        if (ctx) {
          canvas.width = video.videoWidth;
          canvas.height = video.videoHeight;
          ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

          console.log("Captured frame, converting to blob");

          // Convert the canvas to a blob (jpeg format)
          canvas.toBlob((blob) => {
            if (blob) {
              console.log("Blob created, adding to buffer");
              frameBuffer.push(blob);

              // Check if 2 seconds have passed since the last frame was added
              const currentTime = Date.now();
              if (currentTime - lastFrameTime >= 2000) {
                console.log("2 seconds passed, sending to server");

                // Send the buffer to the server for processing
                sendFrameBufferToApi(frameBuffer);
                frameBuffer.length = 0; // Reset the buffer
                lastFrameTime = currentTime;
              }
            } else {
              console.error("Blob conversion failed");
            }
          }, "image/jpeg");
        }
      } else {
        console.log("Video not ready");
      }

      // Call the function again for the next frame
      requestAnimationFrame(processVideo);
    };

    // Function to send the frame buffer to the API and receive the processed frame
    const sendFrameBufferToApi = async (frameBuffer: Blob[]) => {
      const formData = new FormData();
      frameBuffer.forEach((blob, index) => {
        formData.append(`file_${index}`, blob, `frame_${index}.jpg`);
      });

      // Example ref_angle data
      const refr_angle = exercise.ref_angle;
      formData.append("ref_angle", JSON.stringify(refr_angle)); // Send as a JSON string

      try {
        const response = await fetch(
          "http://localhost:8000/process_frame_buffer",
          {
            method: "POST",
            body: formData,
          }
        );

        if (response.ok) {
          const data = await response.json();
          // Process the response data (e.g., update the UI with the result)
          console.log("Processed frame buffer:", data);
          displayProcessedData(data);
        } else {
          console.error("Error processing frame buffer:", response.statusText);
        }
      } catch (error) {
        console.error("Error sending frame buffer to API:", error);
      }
    };

    // Start processing video frames
    requestAnimationFrame(processVideo);
  };

  // Function to handle and display the processed data from the server
  const displayProcessedData = (data: any) => {
    console.log("Received processed data:", data);
    // Implement any UI update or logic based on the processed response (e.g., show the result)
  };

  return (
    <Flex>
      <Box p={8} flexBasis="1/3">
        {/* Chat section */}
      </Box>
      <Box p={8} flexBasis="2/3">
        <Popover>
          <PopoverTrigger>
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
