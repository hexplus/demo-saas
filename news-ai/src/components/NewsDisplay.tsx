import { useContext, useEffect, useState } from 'react';
import { ScrollArea } from '@/components/ui/scroll-area';
import './NewsDisplay.scss';
import {
  CopyCheck,
  ListRestart,
  TextSelect,
  FileMinus,
  Files,
  SquareCheckBig,
  RefreshCcw,
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Separator } from '@/components/ui/separator';
import { StyleSwitcher } from './StyleSwitcher';
import { GlobalContext } from '@/context/GlobalContext';
import { Checkbox } from '@/components/ui/checkbox';
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from '@/components/ui/tooltip';
import { LoadingSpinner } from './LoadingSpinner';
import { FontSwitcher } from './FontSwitcher';

export interface Content {
  text: string;
  type: string;
}

interface NewsDisplayProps {
  title: string;
  content: Content[] | null;
  defaultCollapsed: boolean;
  complete: boolean;
}

export function NewsDisplay({
  content,
  title,
  defaultCollapsed = false,
  complete = true,
}: NewsDisplayProps) {
  const [isCollapsed, setIsCollapsed] = useState(defaultCollapsed);
  const [isChecked, setIsChecked] = useState(false);
  let contentAcummulator = 0;

  const globalContext = useContext(GlobalContext);

  if (!globalContext) {
    throw new Error('GlobalContext is undefined');
  }

  const {
    adapter,
    styles,
    fetchStyles,
    duplicateContent,
    summarize,
    isLoadingContent,
  } = useContext(GlobalContext);

  useEffect(() => {
    fetchStyles();
  }, []);

  return (
    <div
      className={`flex flex-col ${
        complete ? 'h-[calc(100vh-132px)]' : 'h-[calc(100vh-104px)]'
      }`}
    >
      <ScrollArea>
        {content ? (
          <div className="flex flex-1 flex-col">
            <div className="h-auto">
              <div className="flex-1 whitespace-pre-wrap p-4 text-sm">
                <h1 className="news-header">{title}</h1>
                {content.map((item, index) => {
                  contentAcummulator++;
                  if (!complete) {
                    if (contentAcummulator <= 5) {
                      if (item.type === 'h2') {
                        return (
                          <h2 className="news-subheader" key={index}>
                            {item.text.trim()}
                          </h2>
                        );
                      } else if (item.type === 'p') {
                        return (
                          <p className="news-paragraph" key={index}>
                            {item.text.trim()}
                          </p>
                        );
                      }
                    }
                  } else {
                    if (item.type === 'h2') {
                      return (
                        <h2 className="news-subheader" key={index}>
                          {item.text.trim()}
                        </h2>
                      );
                    } else if (item.type === 'p') {
                      return (
                        <p className="news-paragraph" key={index}>
                          {item.text.trim()}
                        </p>
                      );
                    }
                  }
                  return null;
                })}
                {!complete && <p className="news-paragraph">(...)</p>}
              </div>
            </div>
          </div>
        ) : (
          <div className="p-8 text-center text-muted-foreground">
            {isLoadingContent ? <LoadingSpinner /> : ''}
          </div>
        )}
      </ScrollArea>
    </div>
  );
}
