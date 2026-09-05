"""在主机上执行生产队列函数，覆盖未初始化、满队列与成功投递。"""
from pathlib import Path
import subprocess
import tempfile

root = Path(__file__).resolve().parents[1]
source = (root / 'main/boards/esp32-s3n16r8-emoji/emoji_controller.cc').read_text()
start = source.index('bool EmojiController::PlayAnimation(')
end = source.index('\nvoid EmojiController::StopAnimation', start)
implementation = source[start:end]
program = '''
#include <cassert>
#define ESP_LOGE(...)
#define ESP_LOGW(...)
#define pdPASS 1
enum class AnimationType { HAPPY };
struct AnimationMessage { AnimationType type; int param; };
int result = 0, calls = 0, captured = 0;
int xQueueSend(void*, AnimationMessage* msg, int wait) { ++calls; captured=msg->param; assert(wait==0); return result; }
class EmojiController { public: void* animation_queue_ = nullptr; bool PlayAnimation(AnimationType, int); };
''' + implementation + '''
int main() {
 EmojiController c;
 assert(!c.PlayAnimation(AnimationType::HAPPY, 7)); assert(calls==0);
 c.animation_queue_=&c;
 assert(!c.PlayAnimation(AnimationType::HAPPY, 8)); assert(calls==1);
 result=pdPASS;
 assert(c.PlayAnimation(AnimationType::HAPPY, 9)); assert(calls==2); assert(captured==9);
}
'''
with tempfile.TemporaryDirectory() as tmp:
    path=Path(tmp); (path/'test.cc').write_text(program)
    subprocess.run(['c++','-std=c++17',str(path/'test.cc'),'-o',str(path/'test')],check=True)
    subprocess.run([str(path/'test')],check=True)
print('通过：队列未创建、队列已满、成功投递及参数传递')
