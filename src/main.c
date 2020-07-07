#include <stdio.h>
#include "uv.h"
#include <stdlib.h>
#include "logger.h"

#if(WIN32)
#include "windows.h"
#else
#include <unistd.h>
#endif

void
tg_sleep(int32_t time)
{
#if(WIN32)
    Sleep(time*1000);
#else
    sleep(time);
#endif
}
/**
 * reference: https://nikhilm.github.io/uvbook/threads.html
 **/
void hare(void *arg) {
  int tracklen = *((int *) arg);
  while (tracklen) {
    tracklen--;
    tg_sleep(1);
    fprintf(stderr, "Hare ran another step\n");
  }
  fprintf(stderr, "Hare done running!\n");
}

void
init_tg()
{
  logger_initConsoleLogger(stderr);
  logger_setLevel(LogLevel_DEBUG);
  LOG_DEBUG("console logging");
}
int
main() {
  int tracklen = 10;
  uv_thread_t hare_id;
  int status = system("pwd");

  init_tg();
  LOG_INFO("Start Topology Generator, status=%d.\n",status);
  uv_thread_create(&hare_id, hare, &tracklen);

  uv_thread_join(&hare_id);
  return 0;
}
