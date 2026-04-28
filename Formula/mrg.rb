class Mrg < Formula
  include Language::Python::Virtualenv

  desc "Clean miscellaneous files produced by macOS"
  homepage "https://github.com/ilotoki0804/mrg"
  url "https://files.pythonhosted.org/packages/source/m/mrg/mrg-0.2.2.tar.gz"
  sha256 "0eb47533f33b3d2805bf3380323ad9bac158c92d6e0cd2bd993315ce8947f3dc"
  license "Apache-2.0"

  depends_on "python@3.13"

  def install
    virtualenv_install_with_resources
  end

  test do
    (testpath/"sample").mkpath
    (testpath/"sample"/".DS_Store").write("")

    output = shell_output("#{bin}/mrg #{testpath}/sample --ds-store --json")
    assert_match '"ds_store": 1', output
    assert_match '"ds_store_fixed": true', output
    refute_predicate testpath/"sample"/".DS_Store", :exist?
  end
end
