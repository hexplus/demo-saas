// src/components/icons.tsx
import {
  Home,
  Search,
  User,
  Settings,
  Check,
  X,
  Loader2,
  type LucideProps,
} from 'lucide-react';

export const Icons = {
  home: Home,
  search: Search,
  user: User,
  settings: Settings,
  check: Check,
  close: X,
  spinner: Loader2,
};

export type IconName = keyof typeof Icons;
