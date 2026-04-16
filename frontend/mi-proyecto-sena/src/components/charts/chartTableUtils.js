export function getChartColumns(data) {
  if (!data?.length) {
    return [];
  }

  return Object.keys(data[0]);
}
