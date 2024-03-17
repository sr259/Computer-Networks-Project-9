  ---- Infinite List ---
  data Stream a = Cons a (Stream a)
  streamToList :: Stream a-> [a]
  streamToList (Cons x xs) = x : streamToList xs

  ---- Show ---
  instance Show a => Show (Stream a) where
  show stream = "Stream " ++ showPrefix 20 stream
    where
      showPrefix 0 _           = "..."
      showPrefix n (Cons x xs) = show x ++ ", " ++ showPrefix (n - 1) xs

---- streamRepeat ---
 streamRepeat :: a-> Stream a
 streamRepeat x = Cons x (streamRepeat x)

 --- Functor ---
instance Functor Stream where 
    fmap f (Cons x xs) = Cons (f x) (fmap f xs) 

---- streamIterate ---
streamIterate :: (a -> a) -> a -> Stream a
streamIterate f seed = Cons seed (streamIterate f (f seed))

---- streamInterleave ---
streamInterleave :: Stream a -> Stream a -> Stream a
streamInterleave (Cons x xs) y = Cons x (streamInterleave y xs)

---- nats Stream ---
nats :: Stream Integer
nats = streamIterate (\x -> x + 1) 0

---- powersOfTwo
powersOfTwo :: Stream Integer
powersOfTwo = streamIterate (\x -> x * 2) 1

---- triangular ---
 triangular :: Stream Integer
 triangular = streamIterate (\n -> n * (n + 1) `div` 2) 0 



