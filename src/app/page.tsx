"use client";

import { useState } from "react";
import DashboardPage from "./dashboard/page";
import SearchForm from "./components/SearchForm";

export default function AppLayout() {
  const [bodyLocation, setBodyLocation] = useState("");

  return (
    <div>
      <h1>Physiotherapy Treatment App</h1>
      {/* Pass setBodyLocation to SearchForm to update the state when a search is submitted */}
      <SearchForm setBodyLocation={setBodyLocation} />

      {/* Conditionally render DashboardPage only when a search has been performed */}
      {bodyLocation && <DashboardPage bodyLocation={bodyLocation} />}
    </div>
  );
}
