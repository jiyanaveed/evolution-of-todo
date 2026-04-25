/**
 * Main dashboard view modes (same tasks; different presentation in the task panel only).
 */
export const DASHBOARD_THEMES = [
  { id: 'clean', label: 'Clean', description: 'Standard list' },
  { id: 'kanban', label: 'Kanban', description: 'To do and Done' },
  { id: 'adventure', label: 'Adventure', description: 'Quest cards (map on full page)' },
] as const;

export type DashboardThemeId = (typeof DASHBOARD_THEMES)[number]['id'];

export const THEME_STORAGE_KEY = 'momentum-dashboard-theme';

/** Migrate old localStorage values (e.g. removed theme ids) to a valid theme */
export function normalizeStoredTheme(raw: string | null): DashboardThemeId {
  if (raw === 'kanban' || raw === 'adventure' || raw === 'clean') return raw;
  return 'clean';
}
