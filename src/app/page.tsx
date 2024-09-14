"use client";
import SearchForm from "./components/SearchForm";

export default function AppLayout() {
  return (
    <div>
      {/* Pass setUserPrompt to SearchForm to update the state when a search is submitted */}
      <SearchForm />
    </div>
  );
}
