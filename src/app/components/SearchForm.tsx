"use client";

import { useState } from "react";
import { useAction, useMutation } from "convex/react";
import { api } from "../../../convex/_generated/api";
import {
  Center,
  Flex,
  Input,
  Button,
  Icon,
  Spinner,
  Text,
} from "@chakra-ui/react";
import { SearchIcon } from "@chakra-ui/icons";
import { useRouter } from "next/navigation"; // Use Next.js router

export default function SearchForm() {
  const router = useRouter();
  const [userPrompt, setUserPrompt] = useState("");
  const [loading, setLoading] = useState(false);

  const findSimilarExercises = useAction(api.exercises.similarExercises);
  const saveExercises = useMutation(api.exercisesList.createList);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    const exercises = await findSimilarExercises({
      descriptionQuery: userPrompt,
    });

    if (exercises && exercises.length > 0 && exercises[0]?.body_location) {
      const exerciseIds = exercises.map((exercise) => exercise._id);
      await saveExercises({
        exerciseRefs: exerciseIds,
        body_location: exercises[0].body_location,
      });

      router.push(
        `/dashboard?bodyLocation=${exercises[0]?.body_location || ""}`
      );
    } else {
      // Handle the case where no exercises are found
      router.push(`/dashboard?bodyLocation=${userPrompt}`);
    }

    setLoading(false);
  };

  return (
    <Center bg="#E2E8F0" p="4" minH="100vh">
      <Flex direction="column" alignItems="center" gap="8">
        <Text fontSize="4xl" fontWeight="bold">
          My Physio
        </Text>
        <form onSubmit={handleSubmit}>
          <Flex direction="column" alignItems="center" gap="4">
            <Flex alignItems="center" gap="4">
              <Icon as={SearchIcon} />
              <Input
                type="text"
                value={userPrompt}
                onChange={(e) => setUserPrompt(e.target.value)}
                placeholder="Enter your physio needs"
                size="lg"
                rounded="full"
                border="1px solid #E2E8F0" // Added light outline around the search field
                style={{ width: "auto" }} // Adjust the width of the search bar to show all of the placeholder text
              />
              <Button type="submit" size="lg" rounded="full" colorScheme="blue">
                Generate
              </Button>
            </Flex>
            {loading && <Spinner />}
          </Flex>
        </form>
      </Flex>
    </Center>
  );
}
