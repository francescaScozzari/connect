export function highlightSentence(sentence: string, wordsToFind: string[]) {
  if (!wordsToFind?.length) return
  const pattern = new RegExp(`\\b(${wordsToFind.join('|')})\\b`, 'gi')
  const wrappedSentence = sentence.replace(pattern, '<mark>$1</mark>')
  return wrappedSentence
}
