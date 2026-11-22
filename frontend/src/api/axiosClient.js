import axios from "axios";

const API_BASE_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

const axiosClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export const getNotes = async (params = {}) => {
  const response = await axiosClient.get("/notes/", { params });
  return response.data;
};

export const getNoteDetail = async (noteId) => {
  const response = await axiosClient.get(`/notes/${noteId}`);
  return response.data;
};

export const createNote = async (noteData) => {
  const response = await axiosClient.post("/notes/", noteData);
  return response.data;
};

export const linkNotes = async (sourceId, targetId) => {
  const response = await axiosClient.patch(`/notes/${sourceId}/link`, {
    target_id: targetId,
  });
  return response.data;
};

export const getGraphData = async () => {
  const response = await axiosClient.get("/graph/");
  return response.data;
};

export const traverseGraph = async (noteId, params = {}) => {
  const response = await axiosClient.get(`/graph/traverse/${noteId}`, { params });
  return response.data;
};

export const getTagSuggestions = async (query = "") => {
  const response = await axiosClient.get("/tags/suggestions/", {
    params: { query },
  });
  return response.data.tags;
};

export const getDomainAreas = async () => {
  const response = await axiosClient.get("/tags/areas/");
  return response.data.tags;
};

export default axiosClient;
