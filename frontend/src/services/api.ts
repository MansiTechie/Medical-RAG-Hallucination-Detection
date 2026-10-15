import type { AskResponse } from '../types/api';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000";

export class ApiError extends Error {
  statusCode?: number;
  constructor(message: string, statusCode?: number) {
    super(message);
    this.statusCode = statusCode;
    this.name = 'ApiError';
  }
}

export const askMedicalQuestion = async (
  query: string,
  signal?: AbortSignal
): Promise<AskResponse> => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/ask`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query }),
      signal,
    });

    if (!response.ok) {
      if (response.status === 422) {
        throw new ApiError('Invalid request format', 422);
      }
      if (response.status === 503) {
        throw new ApiError('The service is temporarily unavailable due to high demand. Please try again later.', 503);
      }
      if (response.status === 500) {
        throw new ApiError('An unexpected error occurred during the review process.', 500);
      }
      throw new ApiError(`Server returned status ${response.status}`, response.status);
    }

    const data: AskResponse = await response.json();
    return data;
  } catch (error) {
    if (error instanceof ApiError) {
      throw error;
    }
    if (error instanceof Error && error.name === 'AbortError') {
      throw error;
    }
    throw new ApiError('Network error. MedGuide could not complete the evidence review.');
  }
};
