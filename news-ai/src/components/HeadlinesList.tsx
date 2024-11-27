import { useContext, useEffect, useState } from 'react';
import { cn } from '@/lib/utils';
import { ScrollArea } from '@/components/ui/scroll-area';
import { GlobalContext } from '@/context/GlobalContext';
import { LoadingSpinner } from './LoadingSpinner';

interface Headline {
  id: string;
  title: string;
  date: string;
  summary: string;
  body: string;
  slug: string;
  cover: string;
}

export function HeadlinesList() {
  const globalContext = useContext(GlobalContext);

  if (!globalContext) {
    throw new Error('GlobalContext is undefined');
  }

  const { adapter, headlines, isLoadingHeadlines, fetchContent, isProcessing } =
    globalContext;

  const typedHeadlines: Headline[] = headlines?.headlines;
  const [clickedIndex, setClickedIndex] = useState<number | null>(null);

  const handleHeadlineClick = (
    e: React.MouseEvent<HTMLButtonElement>,
    slug: string,
    index: number
  ) => {
    e.preventDefault();
    fetchContent(adapter, slug);
    setClickedIndex(index);
  };

  useEffect(() => {
    setClickedIndex(null);
  }, [typedHeadlines]);

  return (
    <ScrollArea>
      <div className="flex flex-col gap-2 p-4 pt-0 h-auto">
        {isLoadingHeadlines ? (
          <div className={cn('flex h-[52px] items-center justify-center')}>
            <LoadingSpinner />
          </div>
        ) : (
          !typedHeadlines && <>Selecciona una fuente de noticias</>
        )}
        {typedHeadlines &&
          typedHeadlines.map((item, index) => (
            <button
              key={index}
              className={cn(
                'flex flex-col items-start gap-2 rounded-lg border p-3 text-left text-sm transition-all hover:bg-accent',
                clickedIndex === index && 'bg-muted'
              )}
              onClick={(e) => {
                if (adapter.country === 'INT') {
                  window.open(item.url, '_blank');
                } else {
                  handleHeadlineClick(e, item.slug || item.id, index);
                }
              }}
              disabled={isProcessing}
            >
              <div className="flex w-full flex-col gap-1">
                <div className="flex flex-col">
                  <div className="flex gap-2">
                    <div className="font-semibold">{item.title}</div>
                  </div>
                  <div className="ml-auto text-xs text-muted-foreground px-2 items-start pt-1">
                    {item.date}
                  </div>
                </div>
              </div>
              <div className="line-clamp-2 text-xs text-muted-foreground">
                {item.summary.substring(0, 300)}
              </div>
            </button>
          ))}
      </div>
    </ScrollArea>
  );
}
