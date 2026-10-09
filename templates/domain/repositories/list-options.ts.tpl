export interface ListOptions {
  page?: number;
  limit?: number;
  sortBy?: string;
  order?: 'ASC' | 'DESC';
  filters?: Record<string, unknown>;
}

export interface Paginated<T> {
  data: T[];
  total: number;
  page: number;
  limit: number;
}