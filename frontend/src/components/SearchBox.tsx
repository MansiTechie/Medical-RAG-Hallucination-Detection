import React, { useState } from 'react';
import { Search } from 'lucide-react';

interface SearchBoxProps {
  initialQuery?: string;
  onSearch: (query: string) => void;
  isLoading?: boolean;
}

export const SearchBox: React.FC<SearchBoxProps> = ({ initialQuery = '', onSearch, isLoading = false }) => {
  const [query, setQuery] = useState(initialQuery);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim() && !isLoading) {
      onSearch(query);
    }
  };

  return (
    <form className="search-box" onSubmit={handleSubmit}>
      <input
        type="text"
        className="search-input"
        placeholder="What would you like to know?"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        disabled={isLoading}
        aria-label="Search questions"
      />
      <button type="submit" className="search-button" disabled={isLoading} aria-label="Search">
        <Search size={20} />
      </button>
    </form>
  );
};
