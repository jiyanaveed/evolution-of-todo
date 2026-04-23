'use client';

import React from 'react';
import { DASHBOARD_THEMES, type DashboardThemeId } from '../lib/dashboard-themes';

type Props = {
  value: DashboardThemeId;
  onChange: (id: DashboardThemeId) => void;
  layout?: 'grid' | 'row';
};

export default function ThemeSelector({ value, onChange, layout = 'row' }: Props) {
  return (
    <div
      className={layout === 'grid' ? 'grid grid-cols-1 sm:grid-cols-3 gap-2' : 'flex flex-wrap gap-2'}
      role="tablist"
      aria-label="Dashboard theme"
    >
      {DASHBOARD_THEMES.map((t) => {
        const active = value === t.id;
        return (
          <button
            key={t.id}
            type="button"
            role="tab"
            aria-selected={active}
            onClick={() => onChange(t.id as DashboardThemeId)}
            className={[
              'text-left rounded-lg border px-3 py-2 text-sm transition',
              'focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-1',
              active
                ? 'border-indigo-600 bg-indigo-50 text-indigo-900 font-medium shadow-sm'
                : 'border-gray-200 bg-white text-gray-700 hover:border-indigo-300 hover:bg-gray-50',
            ].join(' ')}
          >
            <span className="block font-medium">{t.label}</span>
            <span className="mt-0.5 block text-xs text-gray-500 line-clamp-1">{t.description}</span>
          </button>
        );
      })}
    </div>
  );
}
