"use client";

import {
  Box,
  Heading,
  SimpleGrid,
  Text,
  Card,
  CardBody,
  Image,
  Badge,
  Stack,
  Center,
  Spinner,
  useColorModeValue,
} from "@chakra-ui/react";
import { useSearchParams, useRouter } from "next/navigation";
import { useQuery } from "convex/react";
import { api } from "../../../convex/_generated/api";

// import { Cohere } from "cohere-ai";

export default function DashboardPage() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const bodyLocation = searchParams.get("bodyLocation") || "";

  // Fetch the exercisesList using bodyLocation
  const exercisesList = useQuery(api.exercisesList.getList, {
    body_location: bodyLocation,
  });

  // Get exerciseRefs from exercisesList
  const exerciseIds = exercisesList?.exerciseRefs || [];

  const exercises = useQuery(api.exercises.getExercisesByIds, {
    exerciseIds,
  });

  const bg = useColorModeValue("#F9FAFB", "#1A202C");

  if (!exercisesList || !exercises) {
    return (
      <Center minH="100vh">
        <Spinner size="xl" />
        <h1> No items found</h1>
      </Center>
    );
  }

  return (
    <Box
      p={8}
      bg={bg}
      borderRadius="8px"
      boxShadow="0 4px 12px rgba(0, 0, 0, 0.1)"
    >
      <Heading mb={8} fontSize="4xl" fontWeight="bold" color="#3B3B4F">
        Dashboard - {bodyLocation}
      </Heading>

      {exercises && exercises.length > 0 ? ( // Check if exercises is defined
        <SimpleGrid columns={[1, 2, 3]} spacing={8}>
          {exercises.map(
            (
              exercise // Removed optional chaining
            ) => (
              <Card
                key={exercise._id}
                borderRadius="lg"
                overflow="hidden"
                cursor="pointer"
                onClick={() =>
                  router.push(`/treatment?exerciseId=${exercise._id}`)
                }
                bg="#FFFFFF"
                boxShadow="0 1px 3px rgba(0, 0, 0, 0.1)"
                transition="all 0.3s"
                _hover={{
                  transform: "scale(1.02)",
                  boxShadow: "0 8px 16px rgba(0, 0, 0, 0.2)",
                }}
              >
                <Image
                  src={exercise.file_path}
                  alt={exercise.description}
                  objectFit="cover"
                  height="200px"
                  width="100%"
                  borderRadius="8px 8px 0 0"
                />
                <CardBody p={6}>
                  <Stack spacing={3}>
                    <Text fontWeight="bold" fontSize="xl" color="#3B3B4F">
                      {exercise.description}
                    </Text>
                    <Text color="#6B7280">{exercise.description}</Text>
                    <Badge colorScheme="blue" alignSelf="start">
                      {bodyLocation}
                    </Badge>
                  </Stack>
                </CardBody>
              </Card>
            )
          )}
        </SimpleGrid>
      ) : (
        <Text color="#6B7280">No exercises found yet</Text>
      )}
    </Box>
  );
}
