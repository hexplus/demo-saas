import { useState } from 'react';
import { useInView } from 'react-intersection-observer';

const Image = ({ src, alt, width, height, style = {}, ...props }) => {
  const { ref, inView } = useInView({ triggerOnce: true, threshold: 0.1 });
  const [loaded, setLoaded] = useState(false);

  return (
    <div
      ref={ref}
      style={{
        position: 'relative',
        width,
        height,
        overflow: 'hidden',
        ...style,
      }}
    >
      {!loaded && placeholderSrc && (
        <img
          src={placeholderSrc}
          alt={`Placeholder for ${alt}`}
          style={{
            position: 'absolute',
            width: '100%',
            height: '100%',
            objectFit: 'cover',
            filter: 'blur(20px)',
            transition: 'opacity 0.3s ease-in-out',
            opacity: loaded ? 0 : 1,
          }}
        />
      )}

      {inView && (
        <img
          src={src}
          alt={alt}
          onLoad={() => setLoaded(true)}
          style={{
            width: '100%',
            height: '100%',
            objectFit: 'cover',
            transition: 'opacity 0.3s ease-in-out',
            opacity: loaded ? 1 : 0,
          }}
          {...props}
        />
      )}
    </div>
  );
};

export default Image;
